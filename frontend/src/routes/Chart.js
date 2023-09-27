import { Button } from '@mui/material';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import OutlinedInput from '@mui/material/OutlinedInput';
import Select from '@mui/material/Select';
import {
    CategoryScale,
    Chart as ChartJS,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    TimeScale,
    Title,
    Tooltip
} from 'chart.js';
import 'chartjs-adapter-moment';
import * as React from 'react';
import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';


ChartJS.register(
    CategoryScale,
    LinearScale,
    TimeScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const utcToDatetime = (utcTimestamp) => {
    var date = new Date(utcTimestamp / 1000);
    return date
};

const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: 250,
            width: 250,
        },
    },
};

const chartOptions = {
    scales: {
        x: {
            type: 'time',
            time: {
                unit: 'hour'
            }
        }
    },
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'bottom',
        },
        title: {
            display: true,
            text: 'PNL Chart',
        },
    },
};

const Chart = () => {
    const [chartData, setChartData] = useState(null)
    const [filterOptions, setFilterOptions] = useState(null)
    const [selectedFilters, setSelectedFilters] = useState(null)
    const [filters, setFilters] = useState([])

    const getFilters = async () => {
        const response = await fetch(`http://localhost:8080/get_filter_options`)
        const data = await response.json()
        var emptyFilterOptions = {}
        Object.keys(data).forEach(key => emptyFilterOptions[key] = []);

        setSelectedFilters(emptyFilterOptions)
        setFilterOptions(data)
    }

    const getChartData = async () => {
        setChartData(null)
        const response = await fetch(`http://localhost:8080/get_data`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'filters': JSON.stringify(selectedFilters)
            })
        })

        const jsonResponse = await response.json()
        const data = JSON.parse(jsonResponse)

        var labels = []
        var dataset = []
        for(var key in data) {
            labels.push(utcToDatetime(key))
            dataset.push(data[key])
        }

        setChartData({
            labels,
            datasets: [
                {
                    label: 'PNL Over Time',
                    data: dataset,
                    borderColor: 'rgb(25, 25, 112)',
                    backgroundColor: 'rgba(0, 191, 255, 0.5)',
                    borderWidth: 1,
                    pointRadius: 1,
                    pointHoverRadius: 2
                },
            ],
        })
    }

    const handleFilterChange = (event, key) => {
        const {target: { value }} = event;
        setSelectedFilters(selectedFilters => ({
            ...selectedFilters, 
            [key]: typeof value === 'string' ? value.split(',') : value
        }))
    };

    const handleSetFilters = () => {
        setFilters(selectedFilters)
    }

    useEffect(() => {
        if(filterOptions == null){
            getFilters()
        }        
    })

    useEffect(() => {
        getChartData()
    }, [filters])


    return (
        <div style={{ position: "relative", height: "60vh", width: "80%", margin: "0 auto"}}>
            <h2>Realized PNL</h2>
            {!chartData &&
                <h4>Loading....</h4>
            }
            {chartData &&
                <Line
                    options={chartOptions}
                    data={chartData}
                />
            }
            <div style={{position: "relative", margin: "0 auto"}}>
                {filterOptions && <h3>Filters</h3>}
                {filterOptions &&
                    Object.entries(filterOptions).map(([key, value]) => {
                        return (
                            <FormControl sx={{ m: 1, width: 500 }} key={key + "formControl"}>
                                <InputLabel id="demo-multiple-chip-label" key={key + "inputLable"}>
                                    {key}
                                </InputLabel>
                                <Select
                                    labelId="demo-multiple-chip-label"
                                    id="demo-multiple-chip"
                                    key={key}
                                    multiple
                                    value={selectedFilters[key]}
                                    onChange={(event) => handleFilterChange(event, key)}
                                    input={<OutlinedInput id="select-multiple-chip" label="Chip" />}
                                    renderValue={(selected) => (
                                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                        {selected.map((value) => (
                                        <Chip key={value} label={value} />
                                        ))}
                                    </Box>
                                    )}
                                    MenuProps={MenuProps}
                                >
                                    {value.map((val) => (
                                        <MenuItem
                                            key={val}
                                            value={val}
                                        >
                                            {val}
                                        </MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                        )
                    })
                }
                <br/><br/>
                {filterOptions && 
                    <>
                        <Button onClick={handleSetFilters}>Get Data</Button>
                        <br/>
                        <Button onClick={getFilters}>Clear Filters</Button>
                    </>
                }
            </div>
        </div>
    );
};

export default Chart;

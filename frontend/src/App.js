import './App.css';

import { Routes, Route} from "react-router-dom";
import Chart from "./routes/Chart"

function App() {
  return (    <>
    <Routes>
      <Route path="/" element={<Chart/>}/>
    </Routes>
  </>
  );
}

export default App;

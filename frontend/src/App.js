import Menu from "./components/UI/menu/menu";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./routes/home";
import VideoPage from "./routes/video";


function App() {
  return (
    <div className="App">      
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />}/>
          <Route path="/video" element={<VideoPage />}/>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;

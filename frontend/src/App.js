import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./routes/home";
import VideoPage from "./routes/video";
import LoginPage from "./routes/loginPage";
import RegistrationPage from "./routes/registrationPage";
import AuthContext from "./context/auth";


function App() {

  const [user, setUser] = useState(null);

  useEffect(() => {
    let auth = localStorage.getItem('auth');
    if (auth != null && auth != "") {
      setUser(JSON.parse(auth));
    }
  }, [])

  return (
    <div className="App">     
      <AuthContext.Provider value={{user, setUser}}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<HomePage />}/>
            <Route path="/video" element={<VideoPage />}/>
            <Route path="/login" element={<LoginPage />}/>
            <Route path="/signup" element={<RegistrationPage />}/>
          </Routes>
        </BrowserRouter>
      </AuthContext.Provider>
    </div>
  );
}

export default App;

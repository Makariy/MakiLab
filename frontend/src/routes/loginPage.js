import React, {useContext, useState} from "react";
import Menu from '../components/common/menu/menu';
import LoginForm from "../components/UI/loginForm/loginForm";
import AuthContext from "../context/auth";
import {Navigate} from 'react-router-dom';



const LoginPage = () => {
    const {user} = useContext(AuthContext);

    let next_page = new URLSearchParams(window.location.search).get('next')

    return (
        <React.Fragment>
            {
                user != null ?
                    <Navigate to={!next_page ? "/" : next_page} replace/>
                        :
                    ""
            }
            <Menu />
            <LoginForm />    
        </React.Fragment>
    );
}

export default LoginPage;

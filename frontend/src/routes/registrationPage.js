import React, {useContext, useState} from "react";
import Menu from '../components/common/menu/menu';
import RegistrationForm from "../components/UI/registrationForm/registrationForm";
import AuthContext from "../context/auth";
import {Navigate} from 'react-router-dom';



const RegistrationPage = () => {
    const {user} = useContext(AuthContext);

    return (
        <React.Fragment>
            {
                user != null ?
                    <Navigate to="/" replace/>
                        :
                    ""
            }
            <Menu />
            <RegistrationForm />    
        </React.Fragment>
    );
}

export default RegistrationPage;

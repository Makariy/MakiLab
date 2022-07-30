import React, { useContext, useState } from "react";
import classes from './loginForm.module.css';
import Input from '../../common/UI/input/input';
import { authOnServer } from "../../../API/authorizer";
import AuthContext from "../../../context/auth";
import Loader from "../../common/loader/loader";
import { Link, Navigate } from "react-router-dom";


const LoginForm = () => {
    const {setUser} = useContext(AuthContext);
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const usernameRef = React.createRef();
    const passwordRef = React.createRef();

    
    const onSubmitClicked = (e) => {
        e.preventDefault();
        setIsLoading(true);

        authOnServer(usernameRef.current.value, passwordRef.current.value)
            .then(response => {
                console.log(response);
                setUser(response.user);
                localStorage.setItem('auth', JSON.stringify(response.user));
            })
            .catch(exception => {
                setError(exception.message.error);
                setIsLoading(false)
            });
    }   


    return (
        <React.Fragment>
        {
            isLoading ? 
                <Loader />
                    :
                    <section className={classes.login_section}>
                        <div className={"container " + classes.login_section_container}>
                            <div className={classes.login__inner}>

                                <div className={classes.login__greeting}>
                                    <h3 className={classes.login__greeting_title}>
                                        Login
                                    </h3>
                                </div>
                                <form className={classes.login__form}>
                                    <div className={classes.login__form_inputs}>
                                        <div className={classes.login__form_inputs_item}>
                                            <h5 className={classes.login__form_inputs_item_title}>
                                                Username:
                                            </h5>
                                            <Input ref={usernameRef} placeholder="Enter your username..."/>
                                        </div>
                                        <div className={classes.login__form_inputs_item}>
                                            <h5 className={classes.login__form_inputs_item_title}>
                                                Password:
                                            </h5>
                                            <Input type="password" ref={passwordRef} placeholder="Enter your password..."/>
                                        </div>
                                    </div>
                
                                    <div className={classes.login__form_error}>
                                        <p className={classes.login__form_error_text}>
                                            {error}
                                        </p>
                                    </div>
                
                                    <div className={classes.login__form_footer}>
                                        <div className={classes.login__form_footer_remember}>
                                            <input type="checkbox" className={classes.login__form_footer_remember_checkbox}/>
                                            <p className={classes.login__form_footer_remember_text}>
                                                Remember me
                                            </p>
                                        </div>
                                        <div className={classes.login__form_footer_restore_password}>
                                            <a href="#">
                                                Forgot your password?
                                            </a>
                                        </div>
                                    </div>
                                    <div className={classes.login__form_submit}>
                                        <input value="Login" type="submit" onClick={onSubmitClicked} className={classes.login__form_submit_button}/>
                                    </div>
                                    <div className={classes.login__form_other}>
                                        <Link to="/signup">
                                            Not registered yet?
                                        </Link>
                                    </div>
                                </form>
                            </div>
                        </div>
                </section>
        }
        </React.Fragment>
    );
}

export default LoginForm;


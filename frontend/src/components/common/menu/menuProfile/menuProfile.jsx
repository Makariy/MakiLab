import { useContext } from "react";
import { Link } from "react-router-dom";
import AuthContext from "../../../../context/auth";
import { deauthOnServer } from "../../../../API/authorizer";

import classes from "./menuProfile.module.css";



const MenuProfile = () => {
    const {user, setUser} = useContext(AuthContext);

    const authExit = () => {
        deauthOnServer().then(response => {
            setUser(null);
            localStorage.setItem('auth', null);
        }).catch(exception => {
            setUser(null);
            localStorage.setItem('auth', null);
        })
    }


    return (
        <div className={classes.menu__account}>
            {
                user ? 
                    <div className={classes.menu__account_account}>
                        <Link to="/" replace className={classes.menu__account_account_inner}>
                            <p className={classes.menu__account_account_inner_text}>
                                {user.username}
                            </p>
                        </Link>
                        <button onClick={authExit} className={classes.menu__account_account_exit}>
                            <img src={"/static/media/exit.svg"} className={classes.menu__account_account_exit_img}/>
                        </button>
                    </div>
                        : 
                    <div className={classes.menu__account_login}>
                        <Link to="/login/" replace className={classes.menu__account_login_link}>
                            Login
                        </Link>
                    </div>
            }
        </div>
    );
}

export default MenuProfile;

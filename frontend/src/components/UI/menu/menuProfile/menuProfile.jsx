import { Link } from "react-router-dom";

import classes from "./menuProfile.module.css";


const MenuProfile = () => {
    return (
        <div className={classes.menu__account}>
            <div className={classes.menu__account_login}>
                <Link to="#" className={classes.menu__account_login_link}>
                    Login
                </Link>
            </div>
        </div>
    );
}

export default MenuProfile;

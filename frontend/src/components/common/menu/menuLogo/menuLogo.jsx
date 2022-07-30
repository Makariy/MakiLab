import { Link } from "react-router-dom";
import classes from "./menuLogo.module.css";


const MenuLogo = () => {
    return (
            <div className={classes.menu__logo}>
                <Link to="/" className={classes.menu__logo_link}>
                    Maki<span>Lab</span>
                </Link>
            </div>
    )
}

export default MenuLogo;
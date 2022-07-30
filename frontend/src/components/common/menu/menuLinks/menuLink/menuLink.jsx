import { Link } from "react-router-dom";
import classes from "./menuLink.module.css"


const MenuLink = ({title, href}) => {
    return (
        <li className={classes.menu__list_ul_li}>
            <Link to={href} className={classes.menu__list_ul_li_link}>
                {title}
            </Link>
        </li>
    )
}

export default MenuLink;

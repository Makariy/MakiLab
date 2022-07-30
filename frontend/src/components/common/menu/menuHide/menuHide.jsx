import classes from "./menuHide.module.css";


const MenuHide = ({onMenuHideClicked}) => {
    return (
        <div className={classes.menu__hide}>
            <button onClick={onMenuHideClicked} className={classes.menu__hide_button}>
                <div className={classes.menu__hide_button_stick}></div>
                <div className={classes.menu__hide_button_stick}></div>
                <div className={classes.menu__hide_button_stick}></div>
            </button>
        </div>
    );  
}

export default MenuHide;

import React, { useContext, useState } from "react";
import MenuLinks from "./menuLinks/menuLinks";
import MenuLogo from "./menuLogo/menuLogo";
import MenuProfile from "./menuProfile/menuProfile";
import MenuHide from "./menuHide/menuHide";

import classes from "./menu.module.css";


const Menu = () => {

    const [user, setUser] = useState(null);
    const [isMenuActive, setIsMenuActive] = useState(false);

    const onMenuHideClicked = () => 
        setIsMenuActive(!isMenuActive)
    

    return (
        <React.Fragment>
            <section className={[classes.menu_section, isMenuActive ? classes.active : ""].join(" ")}>
                <div className={"container"}>
                    <div className={classes.menu}>
                        <MenuLogo />
                        <MenuLinks />
                        <MenuProfile />

                        <MenuHide onMenuHideClicked={onMenuHideClicked} />
                    </div>
                </div>
            </section>	
            <section className={classes.mobile_menu_section}>
                <div className={"container"}>
                    <div className={classes.mobile_menu}>
                        <MenuHide onMenuHideClicked={onMenuHideClicked}/>
                        <MenuLogo />
                    </div>
                </div>
            </section>
        </React.Fragment>
    );
}

export default Menu;

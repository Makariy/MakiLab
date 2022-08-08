import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import MenuLinks from "./menuLinks/menuLinks";
import MenuLogo from "./menuLogo/menuLogo";
import MenuProfile from "./menuProfile/menuProfile";
import MenuHide from "./menuHide/menuHide";

import classes from "./menu.module.css";
import MenuSearch from "./menuSearch/menuSearch";


const Menu = ({query, setQuery}) => {

    const [isMenuActive, setIsMenuActive] = useState(false);
    const [isSearchActive, setIsSearchActive] = useState(false);
    let _isMenuActive = isMenuActive;

    const location = useLocation()

    useEffect(
        () => {
            setIsMenuActive(false)
            setIsSearchActive(false)
            setQuery("")
        }, [location]
    )

    const onMenuHideClicked = () => {
        setIsMenuActive(!isMenuActive)
        _isMenuActive = !isMenuActive
        let body_element = document.getElementsByTagName('body')[0];

        if (_isMenuActive)
            body_element.style['overflow-y'] = 'hidden'
        else 
            body_element.style['overflow-y'] = 'auto'

    }

    const onShowSearchClicked = () => {
        setIsSearchActive(!isSearchActive);
    }


    return (
        <React.Fragment>
            <section className={[classes.menu_section, isMenuActive ? classes.active : ""].join(" ")}>
                <div className={"container"}>
                    <div className={classes.menu}>
                        <MenuLogo />
                        <MenuLinks />
                        <div className={classes.menu_section__profile_and_search}>
                            <MenuProfile />
                            <MenuSearch query={query} 
                                setQuery={setQuery} 
                                isActive={isSearchActive}
                                setIsActive={setIsSearchActive}    
                            />
                        </div>
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

import React, { useEffect, useState, useContext } from "react";
import { useLocation } from "react-router-dom";
import SearchContext from "../../../context/search";
import MenuContext from "../../../context/menu";

import MenuLinks from "./menuLinks/menuLinks";
import MenuLogo from "./menuLogo/menuLogo";
import MenuProfile from "./menuProfile/menuProfile";
import MenuHide from "./menuHide/menuHide";

import classes from "./menu.module.css";
import MenuSearch from "./menuSearch/menuSearch";


const Menu = () => {

    const [isMenuActive, setIsMenuActive] = useState(false);
    let _isMenuActive = isMenuActive;

    const location = useLocation()
    const {isSearchActive, setIsSearchActive} = useContext(SearchContext);

    useEffect(
        () => {
            setIsMenuActive(false)
            if (isSearchActive) {
                setIsSearchActive(false)
            }
        }, [location]
    )
    useEffect(
        () => {
            let body_element = document.getElementsByTagName('body')[0];
            
            if (isMenuActive)
                body_element.style['overflow-y'] = 'hidden'
            else 
                body_element.style['overflow-y'] = 'auto'
        }, [isMenuActive]
    )

    const onMenuHideClicked = () => {
        setIsMenuActive(!isMenuActive)    
    }

    const onShowSearchClicked = () => {
        setIsSearchActive(!isSearchActive);
    }


    return (
        <React.Fragment>
            <MenuContext.Provider value={{
                isMenuactive: isMenuActive,
                setIsMenuActive: setIsMenuActive,
            }}>
                <section className={[classes.menu_section, isMenuActive ? classes.active : ""].join(" ")}>
                    <div className={"container"}>
                        <div className={classes.menu}>
                            <MenuLogo />
                            <MenuLinks />
                            <div className={classes.menu_section__profile_and_search}>
                                <MenuProfile />
                                {
                                    setIsSearchActive != null ?
                                        <MenuSearch />
                                            :
                                        ""                                
                                }
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
            </MenuContext.Provider>
        </React.Fragment>
    );
}

export default Menu;

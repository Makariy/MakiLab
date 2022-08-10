import React from "react";


const MenuContext = React.createContext({
    isMenuActive: false,
    setIsMenuActive: null,
});
export default MenuContext;

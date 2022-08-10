import React, { useContext } from "react";
import classes from "./menuSearch.module.css";
import Input from "../../../common/UI/input/input";
import SearchContext from "../../../../context/search";
import MenuContext from "../../../../context/menu";


const MenuSearch = () => {
    const query_ref = React.createRef();
    const {setIsMenuActive} = useContext(MenuContext)
    const {query, setQuery, isSearchActive, setIsSearchActive} = useContext(SearchContext);

    const onSearchButtonClicked = (e) => {
        if (isSearchActive) {
            onSearch(e)
        }
        else {
            setIsSearchActive(true)
        }
    }

    const stopSearch = (e) => {
        e.preventDefault()
        query_ref.current.value = ""
        setQuery("")
        setIsSearchActive(false)
        setIsMenuActive(false)
    }

    const onSearch = (e) => {
        e.preventDefault();
        console.log("Searching")
        let input = query_ref.current.value;
        setQuery(input);
        setIsMenuActive(false); 
    }

    return (
        <div className={classes.menu_search}>
            <form className={[classes.menu_search__form, isSearchActive ? classes.active : ""].join(' ')}>
                <div className={classes.menu_search__input}>
                    <Input ref={query_ref}/>
                    <button onClick={stopSearch} type="button" className={classes.menu_search__close_search}>
                        x
                    </button>
                </div>
                <input onClick={onSearch} type="submit" style={{display: "none"}}/>
            </form>
            <button onClick={onSearchButtonClicked} className={classes.menu_search__search}>
                <img src={"/static/media/search.svg"}/>
            </button>
        </div>
    );
}

export default MenuSearch;

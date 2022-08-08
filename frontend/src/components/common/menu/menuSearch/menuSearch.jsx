import React from "react";
import classes from "./menuSearch.module.css";
import Input from "../../../common/UI/input/input";


const MenuSearch = ({query, setQuery, isActive, setIsActive}) => {
    const query_ref = React.createRef();


    const onSearchButtonClicked = (e) => {
        if (isActive) {
            onSearch(e)
        }
        else {
            setIsActive(true)
        }
    }

    const stopSearch = (e) => {
        e.preventDefault()
        setIsActive(false)
    }

    const onSearch = (e) => {
        e.preventDefault();
        let input = query_ref.current.value;
        setQuery(input);
    }

    return (
        <div className={classes.menu_search}>
            <form className={[classes.menu_search__form, isActive ? classes.active : ""].join(' ')}>
                <div className={classes.menu_search__input}>
                    <Input ref={query_ref}/>
                    <button onClick={stopSearch} className={classes.menu_search__close_search}>
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

import React from "react";


const SearchContext = React.createContext({
    query: "",
    setQuery: null,
    
    isSearchActive: false,
    setIsSearchActive: null,
});
export default SearchContext;

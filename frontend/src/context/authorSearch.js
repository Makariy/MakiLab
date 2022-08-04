import React from "react";


const AuthorSearchContext = React.createContext({
    authors: null,
    setAuthors: null,

    searchQuery: null,
    setSearchQuery: null,

    isLoading: false,
    setIsLoading: null,
});

export default AuthorSearchContext;

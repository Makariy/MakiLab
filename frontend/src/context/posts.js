import React from "react";

const PostsContext = React.createContext({
    author: null,
    setAuthor: null,

    posts: null,
    setPosts: null,

    isLoading: null,
    setIsLoading: null,

    searchQuery: null,
    setSearchQuery: null,

    postMoreActive: null,
    setPostMoreActive: null, 
});

export default PostsContext;


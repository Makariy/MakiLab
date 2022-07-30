import React from "react";


const CreatingContext = React.createContext({
    creatingPost: null,
    setCreatingPost: null,

    isCreating: false,
    setIsCreating: null,

    isRedacting: false,
    setIsRedacting: null,
});

export default CreatingContext;


import React from "react";
import classes from './loader.module.css';


const Loader = () => {
    return (
        <React.Fragment>
            <div className={classes.lds_ring}><div></div><div></div><div></div><div></div></div>
        </React.Fragment>
    );
}

export default Loader;

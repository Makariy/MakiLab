import React, { useState } from "react";
import { Link } from "react-router-dom";
import classes from "./videoPageSelector.module.css";


const VideoPageSelector = ({isLastPage, page}) => {
    const createNewPageLink = (nextPage) => {
        let path = window.location.pathname;
        let params = new URLSearchParams(window.location.search)
        params.set("page", nextPage)        
        return path + "?" + params.toString(); 
    }

    return (
        <div className={classes.video_page_selector}>
            <div className="container">
                <div className={classes.video_page_selector__inner}>
                    <Link to={createNewPageLink(page - 1)} replace>
                        { page > 1 ? "<" : "" }
                    </Link>
                    <Link to={createNewPageLink(page + 1)} replace>
                        { !isLastPage ? ">" : "" }
                    </Link>
                </div>
            </div>
        </div>
    );
}

export default VideoPageSelector;

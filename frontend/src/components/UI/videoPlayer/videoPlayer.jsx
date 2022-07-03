import React, { useState, useEffect } from "react";

import VideoDescription from "./videoDescription/videoDescription";
import classes from "./videoPlayer.module.css";
import { fetchVideos } from "../../../API/fetcher";
import VideoList from "../videoList/videoList";
import Loader from "../../common/loader/loader";


const VideoPlayer = ({video}) => {
    
    return (
        <React.Fragment>
            <section className={classes.video_player_section}>
                <div className={classes.video}>
                    <video className={classes.video_video} controls>
                        <source src={"/videos/videos/" + video.video} type="video/mp4"/>
                    </video>
                    
                    <VideoDescription video={video}/>
                </div>
            </section>
        </React.Fragment>
    );
}

export default VideoPlayer;

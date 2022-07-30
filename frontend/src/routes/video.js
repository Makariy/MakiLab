import React, {  useEffect, useState } from "react";
import "./video.css";

import Menu from "../components/common/menu/menu";
import Footer from "../components/UI/footer/footer";
import Loader from "../components/common/loader/loader";

import VideoPlayer from "../components/UI/videoPlayer/videoPlayer";

import { fetchVideo, fetchVideos } from "../API/fetcher";
import VideoList from "../components/UI/videoList/videoList";

import { usePage } from "../hooks/hooks";
import { useLocation } from "react-router-dom";


const VideoPage = () => {
    // const [user, setUser] = useState(null);

    const location = useLocation()

    const [video, setVideo] = useState(null);
    const [otherVideos, setOtherVideos] = useState(null)
    
    const {page} = usePage()


    useEffect(() => {
        setVideo(null);
        window.scrollTo({top: 0, behavior: "smooth"})
        let video_uuid = new URLSearchParams(location.search).get('video_uuid')

        fetchVideos(page).then(response => 
            setOtherVideos(response.videos.filter(item => item.video.uuid != video_uuid))
        ) 

        fetchVideo(video_uuid).then(response => {
            setVideo(response.video)
            
        })
    }, [location])

    return (
        <React.Fragment>
            <Menu />
            <div className="container">
                    {
                        video != null ? 
                        <div className="player_section">
                            <VideoPlayer video={video}/>            
                            {
                                otherVideos != null ?
                                    <VideoList videos={otherVideos} />
                                        :
                                    <Loader />
                            }
                        </div>
                                :
                            <Loader />
                    }
            </div>
            <Footer />
        </React.Fragment>
    )
}

export default VideoPage;

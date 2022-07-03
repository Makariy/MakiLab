import Video from "./video/video";
import classes from "./videoList.module.css";


const VideoList = ({videos}) => {
    return (
        <section className={classes.videos_section}>
            <div className={"container"}>
                <div className={classes.videos}>
                    {
                        videos.map(item => 
                                    <Video video={item.video} key={item.video.uuid}/>)
                    }
                </div>
            </div>
        </section>
    );
}

export default VideoList;

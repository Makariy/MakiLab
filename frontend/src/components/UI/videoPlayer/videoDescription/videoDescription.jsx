import classes from "./videoDescription.module.css";


const VideoDescription = ({video}) => {
    return (
        <div className={classes.video__text}>
            <h2 className={classes.video__text_title}>
                { video.title }
            </h2>
            <p className={classes.video__text_description}>
                {
                    video.description ?
                        video.description   
                            :
                        "Author doesn't provide any description for this video"        
                }
            </p>
            <p className={classes.video__video_text_views}>
                Views: {video.views}
            </p>
        </div>
    );
}

export default VideoDescription;

import { Link } from "react-router-dom";
import classes from "./video.module.css";


const Video = ({video}) => {

    return (
        <Link className={classes.videos__video} 
              to={"/video/?video_uuid=" + video.uuid}>
            <div className={classes.videos__video_img}>
                <img src={"/videos/previews/" + video.preview} className={classes.videos__video_img_img} />            
            </div>
            <div className={classes.videos__video_text}>
                <h3 className={classes.videos__video_text_title}>
                    {video.title}
                </h3>
                <p className={classes.videos__video_text_text}>
                    {video.description}
                </p>
            </div>
        </Link>
    );
}

export default Video; 

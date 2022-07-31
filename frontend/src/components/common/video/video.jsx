import { useContext } from "react";
import { Link } from "react-router-dom";
import AuthContext from "../../../context/auth";
import classes from "./video.module.css";


const Video = ({video}) => {
    const {user} = useContext(AuthContext);

    const truncateString = (str, len) => {
        let result = str.substr(0, len);
        if (result.length < str.length) 
            result += "...";
        return result;
    }

    return (
        <Link className={classes.videos__video} 
              to={"/video/?video_uuid=" + video.uuid}>
            <div className={classes.videos__video_img}>
                <img src={"/videos/previews/" + video.preview} className={classes.videos__video_img_img} />            
            </div>
            <div className={classes.videos__video_text}>
                <h3 className={classes.videos__video_text_title}>
                    {truncateString(video.title, 45)}
                </h3>
                <p className={classes.videos__video_text_text}>
                    {truncateString(video.description, 75)}
                </p>
            </div>
            {
                video.watched && user ?
                    <div className={classes.videos__video_watched}>
                        <p className={classes.videos__video_watched_text}>
                            Watched
                        </p>        
                    </div>
                        :
                    ""
            }
        </Link>
    );
}

export default Video; 

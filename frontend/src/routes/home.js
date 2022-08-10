import React, {  useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import SearchContext from "../context/search";

import Menu from '../components/common/menu/menu';
import Footer from "../components/UI/footer/footer";
import VideoList from "../components/UI/videoList/videoList";
import Loader from "../components/common/loader/loader";

import { fetchVideos, searchVideos } from "../API/fetcher";
import VideoPageSelector from "../components/UI/videosPageSelector/videoPageSelector";
import { usePage } from "../hooks/hooks";


const HomePage = () => {
    
    const [videos, setVideos] = useState(null);
    const [isLastPage, setIsLastPage] = useState(false);
    const [query, setQuery] = useState("");
    const [isSearchActive, setIsSearchActive] = useState(false);

    const location = useLocation()


    const {page} = usePage()

    useEffect(() => {        
        window.scrollTo({ top: 0, behavior: 'smooth' });
        setVideos(null);

        if (query != "") {
            searchVideos(query).then(response => {
                setVideos(response.videos);
            })
        }
        else {
            fetchVideos(page).then(response => {
                setVideos(response.videos)
                setIsLastPage(response.last)
            });
        }
    }, [location, query]);


    return (
        <React.Fragment>
            <SearchContext.Provider value={{
                query: query,
                setQuery: setQuery,

                isSearchActive: isSearchActive,
                setIsSearchActive: setIsSearchActive
            }}>
                <Menu />
                {
                    videos ? 
                        <VideoList videos={videos}/>
                            :
                        <div style={{marginTop: "10vh", height: "40vh"}} className={"container"}>
                            <Loader />
                        </div>
                }
                <VideoPageSelector page={page} isLastPage={isLastPage}/>
                <Footer />
            </SearchContext.Provider>
        </React.Fragment>
    );
}

export default HomePage;

import axios from "axios";


const checkErrors = (response) => {
    if (response.status != "success") {
        throw Error("Server responded with an error")
    }
    return response;
}


export const fetchVideos = (page) => {
    let url_params = new URLSearchParams({
        page: page 
    })
    return axios.get("/api/videos/get_videos/?" + url_params.toString())
        .then(response => response.data).then(checkErrors);
};

export const fetchVideo = (video_uuid) => {
    let url_params = new URLSearchParams({
        video_uuid: video_uuid
    })
    return axios.get("/api/videos/video/?" + url_params.toString())
        .then(response => response.data).then(checkErrors);
}

export const searchVideos = (query) => {
    let url_params = new URLSearchParams({
        query: query
    })
    return axios.get("/api/videos/search/?" + url_params.toString())
        .then(response => response.data).then(checkErrors);
}

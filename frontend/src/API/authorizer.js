import axios from "axios";
import RequestError from "./exceptions";


const checkResponseError = response => {
    if (response.status != "success") {
        throw new RequestError(response);
    }
    return response
}


export const authOnServer = (username, password) => {
    let data = new FormData();
    data.append('username', username);
    data.append('password', password);

    return axios({
        url: "/api/auth/login/",
        method: "POST",
        data: data
    }).then(response => response.data).then(checkResponseError);
};
 
export const deauthOnServer = () => {
    return axios({
        url: "/api/auth/logout/",
        method: "POST"
    }).then(response => response.data).then(checkResponseError);
}


export const registerOnServer = (username, password, email) => {
    let data = new FormData();
    data.append('username', username);
    data.append('password', password);

    return axios({
        url: "/api/auth/signup/",
        method: "POST",
        data: data
    }).then(response => response.data).then(checkResponseError);
}

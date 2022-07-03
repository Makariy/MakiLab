

export const usePage = () => {
    let page = null 
    let time = null 

    const setPageInStorage = (storagePage) => {
        localStorage.setItem('page', JSON.stringify({
            page: storagePage,
            time: time
        }))
        page = storagePage
    }
    const setTimeInStorage = (storageTime) => {
        localStorage.setItem('page', JSON.stringify({
            page: page,
            time: storageTime
        }))
        time = storageTime
    }
    const getPageAndTimeFromStorage = () => {
        let page = null
        let time = null 

        let storagePage = localStorage.getItem('page')

        if (storagePage == null) 
            return null, null 
    
        storagePage = JSON.parse(storagePage)
        if (storagePage == null) 
            return null, null

        page = storagePage.page 
        time = storagePage.time 
        return [page, time]  
    }

    let urlPage = parseInt(new URLSearchParams(window.location.search).get('page'))

    if (!urlPage) {
        let [storagePage, storageTime]  = getPageAndTimeFromStorage()

        if (storagePage == null || storageTime == null) {
            setPageInStorage(1) 
            setTimeInStorage(new Date().getTime())
        }
        else {
            page = storagePage
            time = storageTime
        }
    }
    else {
        let [storagePage, storageTime] = getPageAndTimeFromStorage()
        if (page != urlPage || time == null) {
            setPageInStorage(urlPage)
            setTimeInStorage(new Date().getTime())
        }
    }
    
    return {
        page: page,
        setPage: setPageInStorage,
        time: time,
        setTime: setTimeInStorage
    }
}

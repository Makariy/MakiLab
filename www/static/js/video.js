
function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
          tmp = item.split("=");
          if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}


function renderVideo(video, page) {
    return `<div class="other__video">
                <a href="/video/?video_uuid=${video.uuid}&page=${page}" class="other__video_video">
                    <img src="/previews/${video.preview}" class="other__video_video-img">
                    <div class="other__video_text">
                        <h3 class="other__video_text-title">
                            ${video.title}
                        </h3>
                        <p class="other__video_text-description">
                            ${video.description}
                        </p>
                    </div>
                </a>
            </div>`;
}


function loadVideos() {
    var page = findGetParameter('page');
    page = page == null ? 1 : parseInt(page);
    $.ajax({
        url: '/videos/get_videos/?page=' + page,
        type: 'GET'
    }).done(function (data) {
        var videos = data.videos;
        console.log(videos);
        for (var i = 0; i < videos.length; i+=1) {
            var rendered = renderVideo(videos[i].video, data.last ? 1 : page + 1);
            document.getElementById('other-videos').innerHTML += rendered;
        }
    });
}


window.onload = loadVideos();

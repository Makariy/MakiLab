
function renderVideo(video) {
    let description = video.description;
    if (description == null)
        description = "Author doesn't provide any description for this video";
    return `
    <a class="videos__video" href="/video/?video_uuid=${video.uuid}">
        <img src="/static/images/${video.preview}" alt=".!." class="videos__video_img">
        <div class="videos__video_text">
            <h3 class="videos__video_text-title">
                ${video.title}
            </h3>
            <p class="videos__video_text-text">
                ${description}
            </p>
        </div>
    </a>
    `
}


function loadVideos() {
    $.ajax({
        type: 'GET',
        url: '/videos/get_videos/',
    }).done(function (response) {
        var videos = $('#videos')[0];
        for (var i = 0; i < response.videos.length; i+=1) {
            videos.innerHTML += renderVideo(response.videos[0].video);
        }
    });
}


window.onload = loadVideos;

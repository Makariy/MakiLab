
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


function renderVideo(video) {
    let description = video.description;
    if (description == null)
        description = "Author doesn't provide any description for this video";
    return `
    <a class="videos__video" href="/video/?video_uuid=${video.uuid}">
        <img src="/previews/${video.preview}" alt=".!." class="videos__video_img">
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


function goToPastPage() {
    page_counter = findGetParameter('page');
    page_counter = page_counter == null ? 1 : parseInt(page_counter);
    if (page_counter > 1)
        document.location.href = document.location.origin + '/?page=' + (page_counter - 1);
}

function goToNextPage() {
    page_counter = findGetParameter('page');
    page_counter = page_counter == null ? 1 : parseInt(page_counter);
    console.log(page_counter);
    document.location.href = document.location.origin + '/?page=' + (page_counter + 1);
}

function loadVideos() {
    page_counter = findGetParameter('page');
    page_counter = page_counter == null ? 1 : parseInt(page_counter);
    $.ajax({
        type: 'GET',
        url: '/videos/get_videos/?page=' + page_counter,
    }).done(function (response) {
        var page = findGetParameter('page') == null ? 1 : parseInt(findGetParameter('page'));
        if (page <= 1) {
            document.getElementById('next-videos-selection--left').style['display'] = 'none';
        }
        if (response.last) {
            document.getElementById('next-videos-selection--right').style['display'] = 'none';
        }
        var videos = $('#videos')[0];
        for (var i = 0; i < response.videos.length; i+=1) {
            videos.innerHTML += renderVideo(response.videos[i].video);
        }
    });
}


window.onload = loadVideos;

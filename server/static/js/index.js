const liveStream = document.getElementById('live-streaming');
document.getElementById('strategy-live').addEventListener('click', () => setStrategy('live'))
document.getElementById('strategy-motion-detection').addEventListener('click', () => setStrategy('motion_detection'))

function setStrategy(strategy) {
    fetch(`/set_strategy/${strategy}`, {
        method: 'GET',
    })
    .then(_data => {
        liveStream.src = `${liveStream.src.split('?')[0]}?t=${new Date().getTime()}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

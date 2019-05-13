class Disease {
    constructor(intensity){
        this.cooldown_interval = null;

        this.active = false;
        this.effect_duration = 0;
        this.cooldown_duration = 0;
        this.description = 0;

        this.setParameters("", intensity, 1, 1, "");
        this.onStatusChange = () => {};
    }

    setParameters(name, intensity, effect, cooldown, description){
        let old_intensity = this.intensity;
        this.name = name;
        this.intensity = intensity;
        this.effect_duration = effect;
        this.cooldown_duration = cooldown;
        this.description = description;
        if (old_intensity === 0 && intensity !== 0){
            this.manifest();
        }
    }

    activateEffect(){
        this.active = true;
        this.onStatusChange(this.name, this.active);

    }
    removeEffect(){
        this.active = false;
        this.onStatusChange(this.name, this.active);
    }

    manifest(){
        if (this.cooldown_interval){
            clearInterval(this.cooldown_interval);
        }
        this.activateEffect();
        this.interval = setInterval(
            this.deactivate.bind(this),
            this.effect_duration
        )
    }

    deactivate(){
        if (this.interval) {
            clearInterval(this.interval);
        }
        this.removeEffect();
        this.cooldown_interval = setInterval(
            this.manifest.bind(this),
            this.cooldown_duration
        )
    }
}

class Parkinson extends Disease{
    constructor(intensity){
        super(intensity);
        this.keyboard = [
            '1234567890-='.split(''),
            'qwertyuiop[]'.split(''),
            [null].concat(('asdfghjkl;\'\\'.split(''))),
            [null].concat(('zxcvbnm,./'.split('')))
        ];
        this.neighbors = [
            [[-1, 0], [-1, -1], [0, -1], [0, 1], [1, 0], [1, -1]],
            [[-1, 0], [-1, 1], [0, -1], [0, 1], [1, 0], [1, 1]]
        ];
    }

    getKeyAtCoordinates(x, y){
        if (x < 0 || y < 0) return null;
        if (y >= this.keyboard.length) return null;
        if (x >= this.keyboard[y].length) return null;

        return this.keyboard[y][x];
    }

    getRandomNearby(x, y){
        let candidates = [];
        this.neighbors[y % 2].forEach(
            (delta) => {
                let n = this.getKeyAtCoordinates(x + delta[1], y + delta[0]);
                if (n !== null){
                    candidates.push(n);
                }
            }
        );
        if (candidates.length === 0) return null;
        return candidates[Math.floor(Math.random()*candidates.length)];
    }

    mangleKey(key){
        if (!this.active) return key;

        let lower = key.toLowerCase();
        let x = -1, y = -1;
        this.keyboard.forEach(
            (row, y_coord) => {
                if (row.includes(lower)){
                    y = y_coord;
                    x = row.indexOf(lower);
                }
            }
        );

        if (x === -1) return key;

        let prob = (this.intensity / 2) / 100;
        let random_neighbor = this.getRandomNearby(x, y);
        return(Math.random() < prob) ? (random_neighbor ? random_neighbor: key) : key;
    }
}

class ADHD extends Disease {
    constructor(intensity){
        super(intensity);
        getJson(editor_urls['adhd_imgs'], (data) => {
            this.image_paths = data;
        });
    }

    activateEffect(){
        super.activateEffect();
        $('#editor-window').hide();
        $("#adhd-img").attr("src", this.image_paths[Math.floor(Math.random()*this.image_paths.length)]);
        $('#dummy-editor-window').show();
    }
    removeEffect(){
        super.removeEffect();
        $("#adhd-img").attr("src", "");
        $('#dummy-editor-window').hide();
        $('#editor-window').show();
    }
}

class Shortsightedness extends Disease{
    activateEffect(){
        super.activateEffect();
        $('#editor-window').find('.editor-char').addClass('editor-char-blurred')
    }

    removeEffect(){
        super.removeEffect();
        $('#editor-window').find('.editor-char').removeClass('editor-char-blurred');
    }
}

class Stutter extends Disease {
    getRepeats(){
        let prob = (this.intensity / 2) / 100;
        return(Math.random() < prob) ? Math.ceil(Math.random() * 4) : 1;
    }
}

class Sleeping extends Disease {
    constructor(props) {
        super(props);
        this.fade_timer = null;
        this.opacity = 0;
    }

    activateEffect(){
        super.activateEffect();
        $('#sleep-overlay').addClass('dimmer');
        let sound = new Howl({
            src: [editor_urls['yawn']],
            format: ['mp3'],
            volume: 0.5,
            onend: function() {
                console.log('Finished!');
            }
        });
        sound.play();
        this.fade_timer = setInterval(() => {
            if (this.opacity < 100){
                this.opacity = this.opacity += 1;
                $('#sleep-overlay').css('opacity', this.opacity / 100);
            } else {
                clearInterval(this.fade_timer);
            }
        }, 30);
    }

    removeEffect(){
        super.removeEffect();
        clearInterval(this.fade_timer);
        this.fade_timer = setInterval(() => {
            if (this.opacity > 0){
                this.opacity = this.opacity -= 1;
                $('#sleep-overlay').css('opacity', this.opacity / 100);
            } else {
                clearInterval(this.fade_timer);
                $('#sleep-overlay').removeClass('dimmer')
            }
        }, 10);
    }
}

class Flu extends Disease{
    constructor(props) {
        super(props);
        this.opacity = 0;
    }

    activateEffect(){
        super.activateEffect();
        this.opacity = 100;
        let sound = new Howl({
            src: [editor_urls['sneeze']],
            format: ['mp3'],
            volume: 0.5,
            onend: function() {
                console.log('Finished!');
            }
        });
        sound.play();
        this.i = setInterval(() => {
            $('#flu-overlay').addClass('flu-snot');
            $('#flu-overlay').css('background-image', 'url(' + editor_urls['snot'] + ')');
            $('#flu-overlay').css('opacity', this.opacity);
            clearInterval(this.i);
        }, 1300);
    }

    removeEffect(){
        super.removeEffect();
        this.fade_timer = setInterval(() => {
            if (this.opacity > 0){
                this.opacity = this.opacity -= 1;
                $('#flu-overlay').css('opacity', this.opacity / 100);
            } else {
                clearInterval(this.fade_timer);
                $('#flu-overlay').removeClass('flu-snot')
            }
        }, 30);
    }
}

messageInput.oninput = function() {
    if (this.value.includes("RED")) {
        alert('Message can not contain substring "RED"');

        while (this.value.includes("RED")) {
            this.value = this.value.replace(/RED/g, '');
        };
    };
};

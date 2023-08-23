import React from 'react';

export default function useLights() {
    const [lights, setLights] = React.useState<any>();

    React.useEffect(() => {
        fetch('http://localhost:5000/lights')
            .then(response => response.json())
            .then(response => {
                setLights(response);
            });
    }, []);

    React.useEffect(() => lights && console.log(lights.filter((item: any) => item.roomName === 'Upstairs Bedroom 1')), [lights]);

    function toggleLight(light_id: number) {
        const light = lights.find((light: any) => light.id === light_id);
        console.log(light)
        fetch('http://localhost:5000/light_value', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                light_id: light_id,
                value: light?.on ? 100 : 0
            })
        }).then(response => {
            if (response.status === 200) {
                setLights((prevState: any) => {
                    const light = prevState.find((light: any) => light.id === light_id);
                    light.on = !light.on;
                    return prevState;
                });
            }
        });
    }

    return { lights, toggleLight };
}
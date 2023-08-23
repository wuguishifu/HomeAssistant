import useLights from "./hooks/useLights";

export default function App() {
    const { lights, toggleLight } = useLights();

    function groupRooms(lights: any): any[] {
        const rooms: any[] = [];
        lights.forEach((light: any) => {
            if (!rooms.some(room => room.roomName === light.roomName)) {
                rooms.push({ roomName: light.roomName, lights: [] });
            }
            rooms.find(room => room.roomName === light.roomName)!.lights.push(light);
        });
        return rooms;
    }

    return (
        <div className="flex flex-col w-full h-screen items-center p-8">
            <h1 className="text-3xl mb-4">Home Assistant</h1>
            {lights && groupRooms(lights).filter(room => room.roomName === 'Upstairs Bedroom 1').map((room: any) => (
                <div className="rounded-xl bg-white px-4 py-2 flex flex-col items-center gap-2" key={room.roomName}>
                    <h2 className="text-xl text-black">{room.roomName}</h2>
                    <div className="flex flex-row gap-8">
                        {room.lights.map((light: any) => (
                            <div
                                className="flex flex-col items-center bg-gray-300 py-4 px-2 rounded-xl"
                                style={{
                                    backgroundColor: light?.value === 100 ? 'yellow' : 'gray'
                                }}
                                key={light.id}
                                onClick={() => toggleLight(light.id)}
                            >
                                <p className="text-black">{light.name}</p>
                            </div>
                        ))}
                    </div>
                </div>
            ))
            }
        </div >
    );
}
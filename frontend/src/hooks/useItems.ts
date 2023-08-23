import React from 'react';

export default function useItems() {

    const [items, setItems] = React.useState<any>();

    React.useEffect(() => {
        fetch('http://localhost:5000/items')
            .then(response => response.json())
            .then(response => setItems(response.filter((item: any) => item.categories?.includes('lights'))));
    }, []);

    return items;

};
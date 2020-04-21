import React from 'react';
import Axios from 'axios';

import CategoryBar from './CategoryBar';
import EventList from './EventList';
import Map from './Map';
import './RecommendationPage.css';

const RecommendationPage = (props) => {
  const { tags = [], isCovid } = props;
  const [
    events,
    setEvents
  ] = React.useState([]);

  const [
    selectedEvent, 
    setSelectedEvent
  ] = React.useState();

  const [temperature, setTemperature] = React.useState();
  const [condition, setCondition] = React.useState();

  React.useEffect(() => {
    Axios.get(
      'http://localhost:5000/conditions'
    ).then(res => {
      const { conditions: { weather, temperature }} = res.data;
      const description = weather.split('-')[1].trim();
      setCondition(description);
      setTemperature(temperature);
    });
  }, []);

  React.useEffect(() => {
    Axios.post(
      'http://localhost:5000/events/recommended',
      {
        tags,
      },
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    ).then(res => {
      setEvents(res.data);
    });
  }, []);

  return (
    <div
      className="recommendation-page"
    >
      {condition !== undefined && temperature !== undefined &&
        <div className='weather-forecast text'>
          Today, you can expect <b>{condition}</b>, with a temperature of <b>{temperature} degrees celcius</b>.
          {
            isCovid && ' Remember to stay safe, stay inside ❤'
          }
        </div>
      }
      <CategoryBar />
      <div className='recommendation-panel'>
        <EventList
          isCovid={isCovid}
          events={events}
          setSelectedEvent={setSelectedEvent}
        />
        <Map
          selectedEvent={selectedEvent}
        />
      </div>
    </div>
  );
};

export default RecommendationPage;

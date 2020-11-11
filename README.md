<p align="center">
  <img src="https://i.ibb.co/Yy97q6w/951cd16b-258f-4143-a4e6-e52fda3fb3da-200x200.png" alt="FastDashLogo-200x200">
</p>

FastDash is an end-to-end dashboard builder designed for rapid visualization and easy sharing. FastDash is designed with busy teams and individuals in mind.

* **Never share Excel files again.** Users can easily share their dashboards with colleagues and clients. Instead of sending a bulky Excel spreadsheet, just send a FastDash URL!
* **Better than Excel PivotCharts** FastDash delivers the power of Excel PivotCharts, but with cleaner, more intuitive UI. Never experience the clunky, decade-old Excel interface again!
* **Simple but beautiful styling** Thanks to FastDash's grid layout and built-in design, uneven margins and incoherent design are never a problem. Focus on truly matters: your dashboard's content.

## Tech Stack
### Backend
* Django with Django Rest Framework
* PostgreSQL is used as RDBMS
* File storage is powered by Amazon S3
* JWT Authentication is supported by `djangorestframework-simplejwt`
* Data analytics is handled with `pandas==1.1.2`
### Frontend
* React and `create-react-app`
* State management is handled by Redux with `redux-thunk`
* FastDash's UI is powered by Bootstrap 4
* Draggable and resizable grid layout system is implemented with `react-grid-layout`
* Dashboard charts are created using ChartistJS with `react-chartist`

## TODO List
1. Support more chart types (e.g. histogram, pie chart)
2. Dashboard styling themes for users to choose from
3. Authentication feature for dashboard share URLs

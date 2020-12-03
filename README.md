<p align="center">
  <img src="https://i.ibb.co/Yy97q6w/951cd16b-258f-4143-a4e6-e52fda3fb3da-200x200.png" alt="FastDashLogo-200x200">
</p>

FastDash is an end-to-end dashboard builder designed for rapid visualization and easy sharing. FastDash is designed with busy teams and individuals in mind.

* **Never share Excel files again.** Users can easily share their dashboards with colleagues and clients. Instead of sending a bulky Excel spreadsheet, just send a FastDash URL!
* **Better than Excel PivotCharts** FastDash delivers the power of Excel PivotCharts, but with cleaner, more intuitive UI. Never experience the clunky, decade-old Excel interface again!
* **Simple but beautiful styling** Thanks to FastDash's grid layout and built-in design, uneven margins and incoherent design are never a problem. Focus on truly matters: your dashboard's content.

## How It Works
1. **Authentication**: When users attempt to login, a request is sent to the Django backend, and is authenticated with `djangorestframework-simplejwt`. Once the user is verified, the JSON Web Token (JWT) access token (which expires in 24 hours) is sent back to the client. The token will be included in all future requests to authorize access to backend data.
2. **Upload Dataset**: Users can upload a CSV file from their local machine, along with a title. After submitting, the dataset will be sent to the Django backend, which would then be uploaded to `AWS S3`. The dataset title along an `S3` link to the file will be pushed to PostgreSQL.
3. **Create Dashboard**: After creating a new dashboard instance, users can start building their own custom dashboard, using the datasets uploaded. A dashboard can utilize multiple datasets at once.
4. **Build Dashboard**: Users can create cards of any size within the 12-column grid, which creates the skeleton of the dashboard. The drag-and-drop functionality is implemented with `react-grid-layout`. There are 3 visualization options: text, bar chart and line graph. The latter two are powered by `react-chartist`. Similar to Excel PivotCharts, users will perform simple data analytics (e.g. mean, sum, max, min, count) to generate the visualization data. This is powered by `pandas` in the backend.
5. **Share Dashboard**: After completing the dashboard, get your dashboard's URL by clicking the `Copy URL` button. Anyone with the URL can view, but cannot edit. And that's it!

## Overview of Tech Stak

### Backend
* Backend Framework: Django with Django Rest Framework (DRF)
* Database: PostgreSQL
* File Storage: AWS S3
* JSON Web Tokens (JWT) Authentication: `djangorestframework-simplejwt`
* Data Analytics: `pandas==1.1.2`
### Frontend
* Frontend Framework: `create-react-app`
* State Management: Redux with `redux-thunk`
* UI Framework: Bootstrap 4
* Interactive Grid: `react-grid-layout`
* Visualization: ChartistJS with `react-chartist`

## Future Plans
1. Support more chart types (e.g. histogram, pie chart)
2. Dashboard styling themes for users to choose from
3. Authentication feature for dashboard share URLs

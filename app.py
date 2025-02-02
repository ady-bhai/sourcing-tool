import streamlit as st
import pandas as pd
from startup_scraper import LinkedInScraper, CrunchbaseScraper, TwitterScraper
from data_processor import StartupProcessor
from datetime import datetime

class StartupSourcingTool:
    def __init__(self):
        st.set_page_config(page_title="Startup Sourcing Tool", layout="wide")
        self.setup_sidebar()
        
    def setup_sidebar(self):
        st.sidebar.title("Startup Sourcing Parameters")
        self.sector = st.sidebar.text_input("Sector (e.g., AI, Healthcare)", "AI")
        self.location = st.sidebar.text_input("Location", "United States")
        self.founding_year = st.sidebar.slider("Founded After Year", 2010, datetime.now().year, 2020)
        self.min_employees = st.sidebar.number_input("Minimum Employees", 1, 1000, 5)
        
    def run(self):
        st.title("Startup Sourcing Tool")
        
        if st.button("Start Search"):
            with st.spinner("Searching for startups..."):
                results = self.search_startups()
                self.display_results(results)
    
    def search_startups(self):
        # Initialize scrapers
        linkedin = LinkedInScraper()
        crunchbase = CrunchbaseScraper()
        twitter = TwitterScraper()
        
        # Collect data from different sources
        results = []
        try:
            linkedin_data = linkedin.search(self.sector, self.location)
            crunchbase_data = crunchbase.search(self.sector, self.location)
            twitter_data = twitter.search(self.sector)
            
            # Process and combine data
            processor = StartupProcessor()
            results = processor.combine_and_filter_results(
                linkedin_data,
                crunchbase_data,
                twitter_data,
                min_year=self.founding_year,
                min_employees=self.min_employees
            )
        except Exception as e:
            st.error(f"Error during search: {str(e)}")
            
        return results
    
    def display_results(self, results):
        if not results:
            st.warning("No startups found matching your criteria.")
            return
            
        # Convert results to DataFrame
        df = pd.DataFrame(results)
        
        # Display summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Startups Found", len(df))
        with col2:
            st.metric("Average Company Size", int(df['employee_count'].mean()))
        with col3:
            st.metric("Average Founded Year", int(df['founded_year'].mean()))
            
        # Display detailed results
        st.dataframe(df)
        
        # Export option
        if st.button("Export to CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="startup_results.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    tool = StartupSourcingTool()
    tool.run()

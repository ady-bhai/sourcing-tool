class StartupProcessor:
    def combine_and_filter_results(self, linkedin_data, crunchbase_data, twitter_data, min_year, min_employees):
        # Combine data from different sources
        combined_results = []
        
        # Process LinkedIn data
        for company in linkedin_data:
            if self._meets_criteria(company, min_year, min_employees):
                combined_results.append(self._format_company_data(company))
                
        # Process Crunchbase data
        for company in crunchbase_data:
            if self._meets_criteria(company, min_year, min_employees):
                combined_results.append(self._format_company_data(company))
                
        # Remove duplicates
        return self._remove_duplicates(combined_results)
    
    def _meets_criteria(self, company, min_year, min_employees):
        return (
            company.get('founded_year', 0) >= min_year and
            company.get('employee_count', 0) >= min_employees
        )
    
    def _format_company_data(self, company):
        return {
            'name': company.get('name'),
            'description': company.get('description'),
            'founded_year': company.get('founded_year'),
            'employee_count': company.get('employee_count'),
            'location': company.get('location'),
            'website': company.get('website'),
            'linkedin_url': company.get('linkedin_url'),
            'crunchbase_url': company.get('crunchbase_url'),
            'twitter_handle': company.get('twitter_handle'),
            'funding': company.get('funding'),
            'investors': company.get('investors')
        }
    
    def _remove_duplicates(self, results):
        # Remove duplicate companies based on name or website
        seen = set()
        unique_results = []
        
        for company in results:
            identifier = company['name'].lower()
            if identifier not in seen:
                seen.add(identifier)
                unique_results.append(company)
                
        return unique_results

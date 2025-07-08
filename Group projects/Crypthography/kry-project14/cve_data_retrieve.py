import json
import urllib.request
import results

def CVE_val(parameter):
    # Construct the URL to fetch JSON data from the NVD database
    distributor = "siemens"
    decoded_distributor = urllib.parse.quote_plus(distributor)

    url = "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=" + decoded_distributor

    # Initialize dictionaries to store CVEs by CPEs and vice versa
    cve_cpes = {}
    cpe_cves = {}
    # Initialize an empty list to store CVE information strings
    cve_info_strings = []

    # Fetch JSON data from the URL and handle any exceptions
    try:
        with urllib.request.urlopen(url) as response:
            # Read the JSON data
            data = response.read().decode("utf-8")
            json_data = json.loads(data)

            # Check if any vulnerability found
            if json_data.get("resultsPerPage") == 0:
                print("No vulnerability has been found for these parameters!")
            else:
                # Iterate over the vulnerabilities in the JSON data
                for vulnerability in json_data["vulnerabilities"]:
                    cve_id = vulnerability["cve"]["id"]
                    base_score = None
                    cvss_version = None

                    # Define CVSS versions to check
                    cvss_versions = ["3.0", "3.1", "2.0"]

                    # Iterate through each version
                    for version in cvss_versions:
                        # Check if the version exists in the vulnerability metrics
                        if f"cvssMetricV{version.replace('.', '')}" in vulnerability["cve"]["metrics"]:
                            cvss_version = version
                            metrics = vulnerability["cve"]["metrics"][f"cvssMetricV{version.replace('.', '')}"]

                            # Iterate through each metric
                            for metric in metrics:
                                # Check if base score is available
                                if "baseScore" in metric["cvssData"]:
                                    base_score = metric["cvssData"]["baseScore"]
                                    break
                        # If base score is found, break out of the loop
                        if base_score is not None:
                            break

                    # If base score is still None, try searching directly in the metrics
                    if base_score is None:
                        for metric in vulnerability["cve"]["metrics"].values():
                            if isinstance(metric, list):
                                for item in metric:
                                    if "baseScore" in item:
                                        base_score = item["baseScore"]
                                        break
                            elif isinstance(metric, dict) and "baseScore" in metric:
                                base_score = metric["baseScore"]
                                break

                    # Check if the parameter represents a port
                    if "port" in parameter:
                        # Print CVE information if the port is found in vulnerability descriptions
                        if "cve" in vulnerability:
                            cve_info = vulnerability["cve"]
                            if "descriptions" in cve_info:
                                descriptions = cve_info["descriptions"]
                                if descriptions:
                                    for description in descriptions:
                                        if "value" in description:
                                            description_value = description["value"]
                                            if parameter in description_value:
                                                index_after_var = description_value.find(parameter) + len(parameter)
                                                if index_after_var < len(description_value) and not description_value[
                                                    index_after_var].isdigit():
                                                    cve_info_string = f"CVE ID: {cve_id}, Base Score ({cvss_version}): {base_score}"
                                                    cve_info_strings.append(cve_info_string)
                    else:
                        # Check if the vulnerability configurations contain CPE matches
                        if "configurations" in vulnerability["cve"]:
                            configurations = vulnerability["cve"]["configurations"]
                            if configurations:
                                for configuration in configurations:
                                    nodes = configuration.get("nodes", [])
                                    if nodes:
                                        for node in nodes:
                                            cpe_matches = node.get("cpeMatch", [])
                                            for cpe_match in cpe_matches:
                                                cpe = cpe_match.get("criteria", "")
                                                # Normalize CPE string and parameter
                                                cpe_normalized = cpe.replace(" ", "_")
                                                parameter_normalized = parameter.replace(" ", "_")
                                                # Check if the parameter exists in the normalized CPE
                                                if parameter_normalized in cpe_normalized:
                                                    if cpe_normalized not in cpe_cves:
                                                        cpe_cves[cpe_normalized] = []
                                                    cpe_cves[cpe_normalized].append((cve_id, base_score, cvss_version))
                                                    for cpe, cves in cpe_cves.items():
                                                        cve_info_strings.append(f"CPE: {cpe}")
                                                        for cve_id, base_score, cvss_version in cves:
                                                            if base_score is not None:
                                                                cve_info_strings.append(f" - CVE ID: {cve_id}, Base Score ({cvss_version}): {base_score}")
                                                            else:
                                                                cve_info_strings.append(f" - CVE ID: {cve_id}, Base Score ({cvss_version}): N/A")

    except Exception as e:
        cve_info_strings.append(f"An error occurred while fetching or parsing JSON data: {e}")

    # # Print CVE information based on the parameter type
    # if "port" in parameter:
    #     for cve_id, data in cve_cpes.items():
    #         base_score = data["base_score"]
    #         cvss_version = data["cvss_version"]
    #         cpes = data["cpes"]
    #         print(f"CVE ID: {cve_id}, Base Score ({cvss_version}): {base_score}")
    #         print("Associated CPEs:")
    #         for cpe in cpes:
    #             print(f" - {cpe}")
    #         print()
    # else:
    #     for cpe, cves in cpe_cves.items():
    #         print(f"CPE: {cpe}")
    #         for cve_id, base_score, cvss_version in cves:
    #             if base_score is not None:
    #                 print(f" - CVE ID: {cve_id}, Base Score ({cvss_version}): {base_score}")
    #             else:
    #                 print(f" - CVE ID: {cve_id}, Base Score ({cvss_version}): N/A")
    #         print()
#
# # Example usage
# CVE_val("windows server", "server 2008")

    results.data["Vulnerabilities"].append(cve_info_strings)
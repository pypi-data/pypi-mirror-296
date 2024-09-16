import json
from collections import Counter
from typing import List, Dict, Any, Optional
import re
import requests
import math
import plotly.graph_objs as go

class NeuroxLink:
    def __init__(self, doi: str, cdn_url="https://cdn.neurolibre.org"):
        self.cdn_url = cdn_url
        self.doi = doi
        self.config_data = self._fetch_config_data()
        self.project_data = self._find_project_by_doi(self.config_data['projects'], self.doi)
        if not self.project_data:
            raise ValueError(f"No project found with DOI: {self.doi}")
        self.data = self._fetch_article_data()
        self.mdast = self.data.get('mdast', {})
        self.node_types = Counter()
        self.headings = []
        self.links = []
        self.code_blocks = []
        self.figures = []
        self.citations = []
        self.parse_mdast(self.mdast)
        doi = f"🌺 {self.doi} 🌺"
        print(doi)
        print(self._create_underline(doi))
        title = self.get_title()
        print(title)
        print(self._create_underline(title))

    def _create_underline(self, text: str) -> str:
        return "〰️" * math.ceil(len(text) / 2)
        
    def _fetch_config_data(self) -> Dict[str, Any]:
        config_url = f"{self.cdn_url}/config.json"
        return self._get_json(config_url)

    def _find_project_by_doi(self, projects: List[Dict[str, Any]], doi: str) -> Optional[Dict[str, Any]]:
        return next((project for project in projects if project.get('doi') == doi), None)

    def _fetch_article_data(self) -> Dict[str, Any]:
        content_url = f"{self.cdn_url}/content/{self.project_data['slug']}/{self.project_data['index']}.json"
        return self._get_json(content_url)

    def _fetch_data(self) -> Dict[str, Any]:
        config_url = f"{self.cdn_url}/config.json"
        config_data = self._get_json(config_url)
        project = self._find_by_doi(config_data['projects'], self.doi)
        if not project:
            raise ValueError(f"No project found with DOI: {self.doi}")
        content_url = f"{self.cdn_url}/content/{project['slug']}/{project['index']}.json"
        return self._get_json(content_url)

    @staticmethod
    def _get_json(url: str) -> Dict[str, Any]:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _find_by_doi(projects: List[Dict[str, Any]], doi: str) -> Optional[Dict[str, Any]]:
        for project in projects:
            if project.get('doi') == doi:
                return project
        return None
        
    def set_cdn_url(self,url):
        self.cdn_url = url
        
    def get_title(self) -> str:
        title = self.project_data.get('title', '')
        subtitle = self.project_data.get('subtitle', '')
        return f"{title}: {subtitle}" if subtitle else title

    def get_license(self) -> Dict[str, Any]:
        return self.project_data.get('license', {})

    def get_authors(self) -> List[Dict[str, Any]]:
        return self.project_data.get('authors', [])

    def get_affiliations(self) -> List[Dict[str, str]]:
        return self.project_data.get('affiliations', [])

    def get_kind(self) -> str:
        return self.data.get('kind', '')

    def get_sha256(self) -> str:
        return self.data.get('sha256', '')

    def get_slug(self) -> str:
        return self.data.get('slug', '')

    def get_location(self) -> str:
        return self.data.get('location', '')

    def get_dependencies(self) -> List[Dict[str, Any]]:
        return self.data.get('dependencies', [])

    def get_frontmatter(self) -> Dict[str, Any]:
        return self.data.get('frontmatter', {})

    def get_github(self) -> str:
        return self.get_frontmatter().get('github', '')

    def get_keywords(self) -> List[str]:
        return self.get_frontmatter().get('keywords', [])

    def get_abbreviations(self) -> Dict[str, str]:
        return self.get_frontmatter().get('abbreviations', {})

    def get_content(self) -> List[Dict[str, Any]]:
        return self.data.get('mdast', {}).get('children', [])

    def get_references(self) -> Dict[str, Any]:
        return self.data.get('references', {})

    def parse_mdast(self, node: Dict[str, Any]):
        if isinstance(node, dict):
            self.node_types[node.get('type', 'unknown')] += 1
            method_name = f"parse_{node.get('type', 'unknown')}"
            parser = getattr(self, method_name, self.parse_default)
            parser(node)
            for value in node.values():
                self.parse_mdast(value)
        elif isinstance(node, list):
            for item in node:
                self.parse_mdast(item)

    def parse_default(self, node: Dict[str, Any]):
        pass

    def parse_heading(self, node: Dict[str, Any]):
        self.headings.append({
            'depth': node.get('depth', 1),
            'text': self.extract_text(node),
            'identifier': node.get('identifier', ''),
        })

    def parse_link(self, node: Dict[str, Any]):
        self.links.append({
            'url': node.get('url', ''),
            'title': node.get('title', ''),
            'text': self.extract_text(node),
        })

    def parse_code(self, node: Dict[str, Any]):
        self.code_blocks.append({
            'lang': node.get('lang', ''),
            'value': node.get('value', ''),
        })

    def parse_container(self, node: Dict[str, Any]):
        if node.get('kind') == 'figure':
            figure_data = self.extract_figure_data(node)
            if figure_data:
                self.figures.append(figure_data)

    def parse_cite(self, node: Dict[str, Any]):
        self.citations.append({
            'label': node.get('label', ''),
            'identifier': node.get('identifier', ''),
            'text': self.extract_text(node),
        })

    def extract_text(self, node: Dict[str, Any]) -> str:
        if 'value' in node:
            return node['value']
        if 'children' in node:
            return ' '.join(self.extract_text(child) for child in node['children'] if isinstance(child, dict))
        return ''

    def extract_figure_data(self, container: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        label = container.get('label', '')
        enumerator = container.get('enumerator', '')
        html_id = container.get('html_id', '')
        
        plotly_data = None
        for child in container.get('children', []):
            if child.get('type') == 'output':
                for data_item in child.get('data', []):
                    if 'data' in data_item:
                        if 'application/vnd.plotly.v1+json' in data_item['data']:
                            plotly_data = data_item['data']['application/vnd.plotly.v1+json']
                            break
                        elif 'application/json' in data_item['data']:
                            json_path = data_item['data']['application/json'].get('path')
                            if json_path:
                                plotly_data = self.fetch_plotly_data(json_path)
                                break
                if plotly_data:
                    break

        return {
            'label': label,
            'enumerator': enumerator,
            'html_id': html_id,
            'plotly_data': plotly_data
        } if plotly_data else None

    def fetch_plotly_data(self, path: str) -> Optional[Dict[str, Any]]:
        url = f"{self.cdn_url}{path}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching Plotly data from {url}: {e}")
            return None

    def get_all_plotly_figures(self) -> List[Dict[str, Any]]:
        plotly_figures = []
        for fig in self.figures:
            if isinstance(fig['plotly_data'], dict) and 'path' in fig['plotly_data']:
                actual_data = self.fetch_plotly_data(fig['plotly_data']['path'])
                if actual_data:
                    fig['plotly_data'] = actual_data
                    plotly_figures.append(fig)
            elif fig['plotly_data'] is not None:
                plotly_figures.append(fig)
        return plotly_figures

    def get_plotly_figure_by_label(self, label: str) -> Optional[Dict[str, Any]]:
        for fig in self.figures:
            if fig['label'] == label:
                if isinstance(fig['plotly_data'], dict) and 'path' in fig['plotly_data']:
                    actual_data = self.fetch_plotly_data(fig['plotly_data']['path'])
                    if actual_data:
                        fig['plotly_data'] = actual_data
                return fig
        return None

    def create_plotly_figure(self, label: str) -> Optional[go.Figure]:
        fig_data = self.get_plotly_figure_by_label(label)
        if fig_data and 'plotly_data' in fig_data:
            plotly_data = fig_data['plotly_data']
            if isinstance(plotly_data, dict):
                if 'content' in plotly_data:
                    return go.Figure(json.loads(plotly_data['content']))
                elif 'data' in plotly_data:
                    return go.Figure(plotly_data['data'])
            elif isinstance(plotly_data, str):
                return go.Figure(json.loads(plotly_data))
        return None

    def extract_caption(self, html_id: str) -> str:
        def search_caption(node):
            if isinstance(node, dict):
                if node.get('type') == 'paragraph':
                    for child in node.get('children', []):
                        if child.get('type') == 'crossReference' and child.get('identifier') == html_id:
                            # Found the reference, now get the text of the paragraph
                            return self.extract_text(node)
                for value in node.values():
                    result = search_caption(value)
                    if result:
                        return result
            elif isinstance(node, list):
                for item in node:
                    result = search_caption(item)
                    if result:
                        return result
            return None

        caption = search_caption(self.mdast)
        return caption if caption else "No caption found"

    def inspect_plotly_figures(self):
        plotly_figures = [fig for fig in self.figures if fig.get('plotly_data')]
        if not plotly_figures:
            print("No Plotly figures found.")
        else:
            print(f"These are the plotly figures I found:")
            print(f"-------------------------------------")
            for fig in plotly_figures:
                label = fig['label']
                enumerator = fig['enumerator']
                html_id = fig['html_id']
                caption = self.extract_caption(html_id)
                print(f"- html-link [{label}] enumerated as (Figure {enumerator})")
                #print(f"  Caption: {caption}")
                print()

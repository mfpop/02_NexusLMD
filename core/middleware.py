from django.template.response import SimpleTemplateResponse

from .processors import process_custom_components


class CustomComponentMiddleware:
    """
    Middleware for processing custom components in the template response
    before they are rendered to the client.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        """
        Process the template response to handle custom components.
        This method is called automatically by Django for middleware classes
        that implement it, after the view has been called but before the 
        template is rendered.
        """
        if isinstance(response, SimpleTemplateResponse):
            # Add a hook to process custom components just before rendering
            old_render = response.render

            def new_render():
                # Call the original render method
                result = old_render()
                
                # Process custom components in the rendered content
                if hasattr(result, 'content') and isinstance(result.content, (str, bytes)):
                    content = result.content.decode() if isinstance(result.content, bytes) else result.content
                    processed_content = process_custom_components(content)
                    if isinstance(result.content, bytes):
                        result.content = processed_content.encode()
                    else:
                        result.content = processed_content
                
                return result

            response.render = new_render
        
        return response
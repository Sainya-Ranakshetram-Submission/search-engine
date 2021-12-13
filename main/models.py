from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField


class StatusCodes(models.IntegerChoices):
    #1xx Informational
    CONTINUE = 100, _('Continue')
    SWITCH_PROTOCOLS = 101, _('Switching protocols')
    PROCESSING = 102, _('Processing')
    EARLY_HINTS = 103, _('Early Hints')
        
    #2xx Succesful
    OK = 200
    CREATED = 201, _('Created')
    ACCEPTED = 202, _('Accepted')
    NON_AUTH = 203, _('Non-Authoritative Information')
    NO_CONTENT=204, _('No Content')
    RESET_CONTENT =205, _('Reset Content')
    PARTIAL_CONTENT=206, _('Partial Content')
    MULTI_STATUS=207, _('Multi-Status')
    ALREADY_REPORTED=208, _('Already Reported')
    IM_USED=226, _('IM Used')
        
    #3xx Redirection
    MULTI_CHOICES = 300, _('Multiple Choices')
    MOVED_PERMANENTLY = 301, _('Moved Permanently')
    FOUND = 302, _('Found (Previously "Moved Temporarily")')
    SEE_OTHER = 303, _('See Other')
    NOT_MODIFIED = 304, _('Not Modified')
    USE_PROXY=305, _('Use Proxy')
    SWITCH_PROXY=306, _('Switch Proxy')
    TEMP_REDIRECT=307, _('Temporary Redirect')
    PERMANENT_REDIRECT=308, _('Permanent Redirect')
        
    #4xx Client Error
    BAD_REQUEST = 400, _('Bad Request')
    UNAUTHORIZED = 401, _('Unauthorized')
    PAY_REQ = 402, _('Payment Required')
    FORBIDDEN = 403, _('Forbidden')
    NOT_FOUND=404, _('Not Found')
    METHOD_NOT_ALLOWED = 405, _('Method Not Allowed')
    NOT_ACCEPTABLE = 406, _('Not Acceptable')
    PROXY_AUTH_REQ = 407, _('Proxy Authentication Required')
    REQUEST_TIMEOUT = 408, _('Request Timeout')
    CONFLICT = 409, _('Conflict')
    GONE=410, _('Gone')
    LENGTH_REQUIRED=411, _('Length Required')
    PRECON_FAILED=412, _('Precondition Failed')
    PAYLOAD_LARGE=413, _('Payload Too Large')
    URL_LONG=414, _('URI Too Long')
    UNSUPPORTED_MEDIA=415, _('Unsupported Media Type')
    UNSATIS_RANGE=416, _('Range Not Satisfiable')
    EXPECTATION_FAILED=417, _('Expectation Failed')
    TEAPOT=418, _("I'm a Teapot")
    MISDIRECTED_REQUEST=421, _('Misdirected Request')
    UNPROCESSABLE_ENTITY=422, _('Unprocessable Entity')
    LOCKED=423, _('Locked')
    FAILED_DEPENDENCY=424, _('Failed Dependency')
    TOO_EARLY=425, _('Too Early')
    UPGRADE_REQ=426, _('Upgrade Required')
    PRECON_REQUIRED=428, _('Precondition Required')
    RATELIMITED=429, _('Too Many Requests')
    HEADER_LARGE=431, _('Request Header Fields Too Large')
    UNAVAILABLE_LEGALLY=451, _('Unavailable For Legal Reasons')
        
    #5xx Server Error
    INTERNAL_SERVER_ERROR = 500, _('Internal Server Error')
    NOT_IMPLEMENTED = 501, _('Not Implemented')
    BAD_GATEWAY=502, _('Bad Gateway')
    SERVICE_UNAVAILABLE=503, _('Service Unavailable')
    GATEWAY_TIMEOUT=504, _('Gateway Timeout')
    VER_HTTP_UNSUPPORTED=505, _('HTTP Version Not Supported')
    VARIANT_ALSO_NEGOTIATES=506, _('Variant Also Negotiates')
    INSUFFICIENT_STORAGE=507, _('Insufficient Storage')
    LOOP_DETECTED=508, _('Loop Detected')
    NOT_EXTENDED=510, _('Not Extended')
    NETWORK_AUTH_REQ=511, _('Network Authentication Required')

class CrawledWebPages(models.Model):
    url = models.CharField(max_length=500,help_text=_('Only domain name'),unique=True)
    title = models.CharField(max_length=500,help_text=_('The Title'),blank=True,null=True)
    sitemap_filepath = models.SlugField(max_length=250,help_text=_('The sitemap.xml file path'),null=True,blank=True)
    robot_txt_filepath = models.SlugField(max_length=250,help_text=_('The robot.txt file path'),null=True,blank=True)
    uses = models.PositiveBigIntegerField(default=0)
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=True,null=True,blank=True)
    http_status = models.IntegerField(default=StatusCodes.OK, choices=StatusCodes.choices)
    scan_internal_links=models.BooleanField(default=True)
    
    keywords_meta_tags = ArrayField(models.CharField(max_length=500),null=True,blank=True,default=list)
    keywords_in_site = ArrayField(models.CharField(max_length=500),null=True,blank=True,default=list)
    
    stripped_request_body = models.TextField(null=True,blank=True,help_text=_('Mainly the description to display'))
    
    keywords_ranking=models.JSONField(null=True,blank=True,default=dict)
    last_crawled=models.DateTimeField(default=now)
    
    def __str__(self):
        return self.url
    
    def save(self,*args,**kwargs):
        self.last_crawled = now()
        if self.url.startswith('https://') or self.url.startswith('http://'):
            self.url = self.url.replace('https://','')
            self.url = self.url.replace('http://','')
            self.url = self.url.strip()
        if self.url.startswith('www.'):
            self.url = self.url.replace('www.','')
            self.url = self.url.strip()
        self.url = self.url.strip('/')
        super().save(*args,**kwargs)
    
    class Meta:
        ordering = ("uses",)
        verbose_name_plural = _('Crawled Web Pages')
        indexes = [
            models.Index(fields=['url'],name="url_idx",include=['uses']),
        ]


class ToBeCrawledWebPages(models.Model):
    url = models.CharField(max_length=250,help_text=_('Only domain name'),unique=True)
    scan_internal_links=models.BooleanField(default=True)
    http_status = models.IntegerField(default=StatusCodes.OK, choices=StatusCodes.choices)
    last_crawled=models.DateTimeField(default=now)
    
    def __str__(self):
        return self.url
    
    def save(self,*args,**kwargs):
        self.last_crawled = now()
        if self.url.startswith('https://') or self.url.startswith('http://'):
            self.url = self.url.replace('https://','')
            self.url = self.url.replace('http://','')
            self.url = self.url.strip()
        if self.url.startswith('www.'):
            self.url = self.url.replace('www.','')
            self.url = self.url.strip()
        self.url = self.url.strip('/')
        super().save(*args,**kwargs)
    
    class Meta:
        ordering = ("last_crawled", )
        verbose_name_plural = _('To Be Crawled Web Pages')
        indexes = [
            models.Index(fields=['url','http_status'],name="url_and_http_status_idx",include=['last_crawled']),
        ]
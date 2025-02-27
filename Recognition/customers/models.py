from django.db import models
from django.db.models.functions import datetime
from django.templatetags.tz import utc
from django.utils import timezone


def time_delta_format(value):
    delta = int((datetime.datetime.now(tz=timezone.utc) - value).total_seconds() + 21600)
    dividers = {'second': 60, 'minute': 60, 'hour': 24, 'day': 7, 'week': 4, 'month': 12, 'year': 12}
    if delta == 0:
        return 'Just now'
    for key in dividers.keys():
        if delta < dividers[key]:
            return f'{delta} {key}{(delta != 1) * "s"} ago'
        delta //= dividers[key]


class Customer(models.Model):
    passport = models.ForeignKey('Passport', on_delete=models.CASCADE)
    address = models.CharField(max_length=64, null=True, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    email = models.CharField(max_length=32, null=True, blank=True)
    created = models.DateTimeField()
    objects = models.Manager()

    @property
    def created_delta(self):
        return time_delta_format(self.created)

    def __str__(self):
        passport = Passport.objects.get(pk=self.passport.id)
        return f'{passport.surname.title()} {passport.given_name.title()}'

    class Meta:
        app_label = 'customers'
        db_table = 'customer'
        verbose_name = 'Customer'


class Passport(models.Model):
    issuer_code = models.CharField(max_length=3)
    surname = models.CharField(max_length=32)
    given_name = models.CharField(max_length=32)
    document_number = models.CharField(max_length=9)
    nationality_code = models.CharField(max_length=3)
    birth_date = models.DateField()
    sex = models.CharField(choices=[('m', 'M'), ('f', 'F')], default='M', max_length=1)
    expiry_date = models.DateField()
    optional_data_1 = models.CharField(max_length=14, null=True, blank=True)
    optional_data_2 = models.CharField(max_length=14, null=True, blank=True)
    page_scan = models.ManyToManyField('PageScan')
    created = models.DateTimeField()
    objects = models.Manager()

    @property
    def created_delta(self):
        return time_delta_format(self.created)

    def __str__(self):
        return f'{self.surname.title()} {self.given_name.title()}'

    class Meta:
        app_label = 'customers'
        db_table = 'passport'
        verbose_name = 'Passport'


class PageScan(models.Model):
    image = models.ImageField()
    mrz_text = models.CharField(max_length=96, null=True)
    created = models.DateTimeField()
    objects = models.Manager()

    @property
    def created_delta(self):
        return time_delta_format(self.created)

    def __str__(self):
        try:
            passport = Passport.objects.filter(page_scan=self)[0]
            return f'{passport.surname.title()} {passport.given_name.title()} ({self.id})'
        except IndexError:
            return f'[Unknown Scan {self.id}]'

    class Meta:
        app_label = 'customers'
        db_table = 'pagescan'
        verbose_name = 'Page Scan'


state_code = {
    'ABW': 'Aruba',
    'AFG': 'Afghanistan',
    'AGO': 'Angola',
    'AIA': 'Anguilla',
    'ALA': 'Åland Islands',
    'ALB': 'Albania',
    'AND': 'Andorra',
    'ARE': 'United Arab Emirates',
    'ARG': 'Argentina',
    'ARM': 'Armenia',
    'ASM': 'American Samoa',
    'ATA': 'Antarctica',
    'ATF': 'French Southern Territories',
    'ATG': 'Antigua and Barbuda',
    'AUS': 'Australia',
    'AUT': 'Austria',
    'AZE': 'Azerbaijan',
    'BDI': 'Burundi',
    'BEL': 'Belgium',
    'BEN': 'Benin',
    'BES': 'Bonaire, Sint Eustatius and Saba',
    'BFA': 'Burkina Faso',
    'BGD': 'Bangladesh',
    'BGR': 'Bulgaria',
    'BHR': 'Bahrain',
    'BHS': 'Bahamas',
    'BIH': 'Bosnia and Herzegovina',
    'BLM': 'Saint Barthélemy',
    'BLR': 'Belarus',
    'BLZ': 'Belize',
    'BMU': 'Bermuda',
    'BOL': 'Bolivia, Plurinational State of',
    'BRA': 'Brazil',
    'BRB': 'Barbados',
    'BRN': 'Brunei Darussalam',
    'BTN': 'Bhutan',
    'BVT': 'Bouvet Island',
    'BWA': 'Botswana',
    'CAF': 'Central African Republic',
    'CAN': 'Canada',
    'CCK': 'Cocos (Keeling) Islands',
    'CHE': 'Switzerland',
    'CHL': 'Chile',
    'CHN': 'China',
    'CIV': 'Côte d\'Ivoire',
    'CMR': 'Cameroon',
    'COD': 'Congo, Democratic Republic of the',
    'COG': 'Congo',
    'COK': 'Cook Islands',
    'COL': 'Colombia',
    'COM': 'Comoros',
    'CPV': 'Cabo Verde',
    'CRI': 'Costa Rica',
    'CUB': 'Cuba',
    'CUW': 'Curaçao',
    'CXR': 'Christmas Island',
    'CYM': 'Cayman Islands',
    'CYP': 'Cyprus',
    'CZE': 'Czechia',
    'DEU': 'Germany',
    'DJI': 'Djibouti',
    'DMA': 'Dominica',
    'DNK': 'Denmark',
    'DOM': 'Dominican Republic',
    'DZA': 'Algeria',
    'ECU': 'Ecuador',
    'EGY': 'Egypt',
    'ERI': 'Eritrea',
    'ESH': 'Western Sahara',
    'ESP': 'Spain',
    'EST': 'Estonia',
    'ETH': 'Ethiopia',
    'FIN': 'Finland',
    'FJI': 'Fiji',
    'FLK': 'Falkland Islands (Malvinas)',
    'FRA': 'France',
    'FRO': 'Faroe Islands',
    'FSM': 'Micronesia, Federated States of',
    'GAB': 'Gabon',
    'GBR': 'United Kingdom of Great Britain and Northern Ireland',
    'GEO': 'Georgia',
    'GGY': 'Guernsey',
    'GHA': 'Ghana',
    'GIB': 'Gibraltar',
    'GIN': 'Guinea',
    'GLP': 'Guadeloupe',
    'GMB': 'Gambia',
    'GNB': 'Guinea-Bissau',
    'GNQ': 'Equatorial Guinea',
    'GRC': 'Greece',
    'GRD': 'Grenada',
    'GRL': 'Greenland',
    'GTM': 'Guatemala',
    'GUF': 'French Guiana',
    'GUM': 'Guam',
    'GUY': 'Guyana',
    'HKG': 'Hong Kong',
    'HMD': 'Heard Island and McDonald Islands',
    'HND': 'Honduras',
    'HRV': 'Croatia',
    'HTI': 'Haiti',
    'HUN': 'Hungary',
    'IDN': 'Indonesia',
    'IMN': 'Isle of Man',
    'IND': 'India',
    'IOT': 'British Indian Ocean Territory',
    'IRL': 'Ireland',
    'IRN': 'Iran, Islamic Republic of',
    'IRQ': 'Iraq',
    'ISL': 'Iceland',
    'ISR': 'Israel',
    'ITA': 'Italy',
    'JAM': 'Jamaica',
    'JEY': 'Jersey',
    'JOR': 'Jordan',
    'JPN': 'Japan',
    'KAZ': 'Kazakhstan',
    'KEN': 'Kenya',
    'KGZ': 'Kyrgyzstan',
    'KHM': 'Cambodia',
    'KIR': 'Kiribati',
    'KNA': 'Saint Kitts and Nevis',
    'KOR': 'Korea, Republic of',
    'KWT': 'Kuwait',
    'LAO': 'Lao People\'s Democratic Republic',
    'LBN': 'Lebanon',
    'LBR': 'Liberia',
    'LBY': 'Libya',
    'LCA': 'Saint Lucia',
    'LIE': 'Liechtenstein',
    'LKA': 'Sri Lanka',
    'LSO': 'Lesotho',
    'LTU': 'Lithuania',
    'LUX': 'Luxembourg',
    'LVA': 'Latvia',
    'MAC': 'Macao',
    'MAF': 'Saint Martin (French part)',
    'MAR': 'Morocco',
    'MCO': 'Monaco',
    'MDA': 'Moldova, Republic of',
    'MDG': 'Madagascar',
    'MDV': 'Maldives',
    'MEX': 'Mexico',
    'MHL': 'Marshall Islands',
    'MKD': 'North Macedonia',
    'MLI': 'Mali',
    'MLT': 'Malta',
    'MMR': 'Myanmar',
    'MNE': 'Montenegro',
    'MNG': 'Mongolia',
    'MNP': 'Northern Mariana Islands',
    'MOZ': 'Mozambique',
    'MRT': 'Mauritania',
    'MSR': 'Montserrat',
    'MTQ': 'Martinique',
    'MUS': 'Mauritius',
    'MWI': 'Malawi',
    'MYS': 'Malaysia',
    'MYT': 'Mayotte',
    'NAM': 'Namibia',
    'NCL': 'New Caledonia',
    'NER': 'Niger',
    'NFK': 'Norfolk Island',
    'NGA': 'Nigeria',
    'NIC': 'Nicaragua',
    'NIU': 'Niue',
    'NLD': 'Netherlands, Kingdom of the',
    'NOR': 'Norway',
    'NPL': 'Nepal',
    'NRU': 'Nauru',
    'NZL': 'New Zealand',
    'OMN': 'Oman',
    'PAK': 'Pakistan',
    'PAN': 'Panama',
    'PCN': 'Pitcairn',
    'PER': 'Peru',
    'PHL': 'Philippines',
    'PLW': 'Palau',
    'PNG': 'Papua New Guinea',
    'POL': 'Poland',
    'PRI': 'Puerto Rico',
    'PRK': 'Korea, Democratic People\'s Republic of',
    'PRT': 'Portugal',
    'PRY': 'Paraguay',
    'PSE': 'Palestine, State of',
    'PYF': 'French Polynesia',
    'QAT': 'Qatar',
    'REU': 'Réunion',
    'ROU': 'Romania',
    'RUS': 'Russian Federation',
    'RWA': 'Rwanda',
    'SAU': 'Saudi Arabia',
    'SDN': 'Sudan',
    'SEN': 'Senegal',
    'SGP': 'Singapore',
    'SGS': 'South Georgia and the South Sandwich Islands',
    'SHN': 'Saint Helena, Ascension and Tristan da Cunha',
    'SJM': 'Svalbard and Jan Mayen',
    'SLB': 'Solomon Islands',
    'SLE': 'Sierra Leone',
    'SLV': 'El Salvador',
    'SMR': 'San Marino',
    'SOM': 'Somalia',
    'SPM': 'Saint Pierre and Miquelon',
    'SRB': 'Serbia',
    'SSD': 'South Sudan',
    'STP': 'Sao Tome and Principe',
    'SUR': 'Suriname',
    'SVK': 'Slovakia',
    'SVN': 'Slovenia',
    'SWE': 'Sweden',
    'SWZ': 'Eswatini',
    'SXM': 'Sint Maarten (Dutch part)',
    'SYC': 'Seychelles',
    'SYR': 'Syrian Arab Republic',
    'TCA': 'Turks and Caicos Islands',
    'TCD': 'Chad',
    'TGO': 'Togo',
    'THA': 'Thailand',
    'TJK': 'Tajikistan',
    'TKL': 'Tokelau',
    'TKM': 'Turkmenistan',
    'TLS': 'Timor-Leste',
    'TON': 'Tonga',
    'TTO': 'Trinidad and Tobago',
    'TUN': 'Tunisia',
    'TUR': 'Türkiye',
    'TUV': 'Tuvalu',
    'TWN': 'Taiwan, Province of China',
    'TZA': 'Tanzania, United Republic of',
    'UGA': 'Uganda',
    'UKR': 'Ukraine',
    'UMI': 'United States Minor Outlying Islands',
    'URY': 'Uruguay',
    'USA': 'United States of America',
    'UZB': 'Uzbekistan',
    'VAT': 'Holy See',
    'VCT': 'Saint Vincent and the Grenadines',
    'VEN': 'Venezuela, Bolivarian Republic of',
    'VGB': 'Virgin Islands (British)',
    'VIR': 'Virgin Islands (U.S.)',
    'VNM': 'Viet Nam',
    'VUT': 'Vanuatu',
    'WLF': 'Wallis and Futuna',
    'WSM': 'Samoa',
    'YEM': 'Yemen',
    'ZAF': 'South Africa',
    'ZMB': 'Zambia',
    'ZWE': 'Zimbabwe',
}

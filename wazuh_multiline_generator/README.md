# Required configurations

## Monitoring the file

Add a group to forward log collection configurtions

```
<agent_config>
	<localfile>
		<location>C:\app\logs\out.log</location>
		<log_format>multi-line-regex</log_format>
		<multiline_regex replace="wspace" match="start">endpoint:/</multiline_regex>
	</localfile>
</agent_config>

<decoder name="custom-webapp">
    <prematch>^endpoint:/</prematch>
</decoder>
```

## Decoders

To process the logs use the following decoders

```
<decoder name="custom-webapp">
    <prematch>^endpoint:/</prematch>
</decoder>

<decoder name="custom-webapp">
    <parent>custom-webapp</parent>
    <regex>^endpoint:/serv-login-service-5.5.0-ann(\.*)\s+</regex>
    <order>url.endpoint</order>
</decoder>

<decoder name="custom-webapp">
    <parent>custom-webapp</parent>
    <regex>RequestDateTime:\s(\d\d/\d\d/\d\d\d\d\s\d\d:\d\d:\d\d) </regex>
    <order>url.timestamp</order>
</decoder>

<decoder name="custom-webapp">
    <parent>custom-webapp</parent>
    <regex>x-responsetime:(\d+),</regex>
    <order>url.requesttime</order>
</decoder>
```


## Rules 

To trigger alerts use the following rules

```
<group name="custom_webapp,">
	<rule id="100201" level="3">
		<decoded_as>custom-webapp</decoded_as>
		<description>Custom WebAPP log</description>
	</rule>
</group>

<group name="custom_webapp,">
	<rule id="100202" level="4">
		<if_sid>100201</if_sid>
		<field name="url.requesttime">2\d\d+</field>
		<description>Custom WebAPP log</description>
	</rule>
</group>
```
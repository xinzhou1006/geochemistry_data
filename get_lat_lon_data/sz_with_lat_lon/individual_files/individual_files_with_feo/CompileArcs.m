%Compile filtered arc segments into a single output file formatted for
%further processing/data analysis via PetroPlot
clear all
for Type=1:4  %Types of filters, see GlobalArcVolcFilter

    if Type == 1
        String1='GlobalArcs6Vals.xls';
        String2='GlobalVolcAverages6Vals.xls';
    elseif Type == 2
        String1='GlobalArcsMg55Vals.xls';
        String2='GlobalVolcAveragesMg55Vals.xls';  
    elseif Type == 3
        String1='GlobalArcsMg60Vals.xls';
        String2='GlobalVolcAveragesMg60Vals.xls';  
    elseif Type == 4
        String1='GlobalArcsRawVals.xls';
        String2='GlobalVolcAveragesRawVals.xls';  
    end
SegmentNames=importdata('SegmentNames.xls');
MyHeaders = importdata('Headers.xls');
%Below you can add any function columns to be included in analyses, Make
%sure to add functions in GlobalArcVolcFilt as well 
AddColumns=[{'Mg#'} {'Eu/Eu*'} {'Eu/Eu**'} {'ASI'} {'Dy/Yb'} {'Li/Y'} {'Zr/Nb'} {'Nb/Ta'} {'Rb/Nb'} {'Ba/Nb'} {'Rb/Cs'} {'Nb/Zr'} {'Pb/Nb'} {'Cs/Nb'} {'La/Nb'}...
    {'La/Zr'} {'Th/Nb'} {'Th/Zr'} {'La/Yb'} {'La/Sm'} {'Pb/Ce'} {'Pb/La'} {'Ba/La'} {'Sm/La'} {'Th/La'} {'Zr/Sm'} {'Zr/Hf'} {'Zr/Ti'} {'Sr/Nd'} {'Sm/Nd'} {'Th/U'} {'Gd/Yb'} {'Sr/Zr'}];  
ArcCompilation=cell(1,length(MyHeaders)+length(AddColumns));
LastCol=find(strcmpi(MyHeaders(1,:),'HF176_HF177')); %Designates final column prior to 6-values
ArcCompilation(1,:)=[MyHeaders(1:LastCol) AddColumns MyHeaders(LastCol+1:end)];

for i=1:length(SegmentNames)
    CurrentSeg=SegmentNames{i}
    MySeg=GlobalArcVolcFilter(CurrentSeg,MyHeaders,AddColumns, Type);
    ArcCompilation=[ArcCompilation; MySeg(2:end,:)];
end

%Below is formatting for PetroPlot
VolcanoNum=cell(size(ArcCompilation,1),1);
ArcNum=cell(size(ArcCompilation,1),1);
VolcanoCounter=0;
ArcCounter=0;
for i=2:size(ArcCompilation,1)
    if strcmpi(ArcCompilation{i,1},ArcCompilation{i-1,1})==0
        ArcCounter=ArcCounter+1;
    end
    if strcmpi(ArcCompilation{i,2},ArcCompilation{i-1,2})==0
        VolcanoCounter=VolcanoCounter+1;
    end
    VolcanoNum{i}=VolcanoCounter;
    ArcNum{i}=ArcCounter;
end
[~,~,MetaData] = xlsread(['VolcanoMetaData.xls']);

FinalCompOut=[ArcCompilation(:,2) VolcanoNum ArcCompilation(:,1) ArcNum ArcCompilation(:,3:end)];
%code below adds metadata to full output
MyMeta1=MetaData(1,:);
for i=2:size(FinalCompOut,1)
    Newline=MetaData(find(strcmpi(MetaData(:,1),FinalCompOut{i,1})),:);
    if size(Newline,1)==0
        Newline=cell(1,25);
    end
    if isempty(Newline{1,1})
         Newline{1,1}='No MetaData Available';
    end
    MyMeta1=[MyMeta1; Newline];
end
FinalCompOut=[FinalCompOut MyMeta1];

FinalCompOut{1,2}='VolcanoNum';   
FinalCompOut{1,4}='ArcNum';       

if exist(String1, 'file')==2  %delete prior files to avoid corrupt outputs
    delete(String1)
end
xlswrite(String1,FinalCompOut)

%Code below takes averages of volcanos and outputs file ready for
%PetroPlot.  For ratios, averages are only included if there are at least
%two values, for 6 values, single values are allowed.
SiO2Col=find(strcmpi(FinalCompOut(1,:),'SIO2(WT%)'));
locstart=find(strcmpi(FinalCompOut(1,:),'LONGITUDE (MIN.)'));
locend=find(strcmpi(FinalCompOut(1,:),'LATITUDE (MAX.)'));
AddColStart=find(strcmpi(FinalCompOut(1,:),AddColumns{1}));
[Arc_num,Arc_txt,Arc_FullDat] = xlsread([String1]); 
VolcRangeStart=1;
VolcAverages=FinalCompOut(1,:);
for i=3:size(ArcCompilation,1)
    if strcmpi(ArcCompilation{i,2},ArcCompilation{i-1,2})==0
        VolcRangeEnd=i-2;
        VolcAverages=[VolcAverages; [FinalCompOut(VolcRangeStart+1,1:SiO2Col-1) num2cell(nanmean(Arc_num(VolcRangeStart:VolcRangeEnd,SiO2Col-1:end),1))]];
        for j=1:length(AddColumns)
            TotalValues=(VolcRangeEnd-VolcRangeStart+1)-sum(isnan(Arc_num(VolcRangeStart:VolcRangeEnd,AddColStart+j-2))); %Total non-nan values for each ratio/function
            if TotalValues<2 %Only average ratios/functions with at least two values
                VolcAverages{end,AddColStart+j-1}=NaN;
            end
        end        
        VolcRangeStart=VolcRangeEnd+1;            
    end
end
VolcRangeEnd=i-1; %Copy in final volcano average...
VolcAverages=[VolcAverages; [FinalCompOut(VolcRangeStart+1,1:SiO2Col-1) num2cell(nanmean(Arc_num(VolcRangeStart:VolcRangeEnd,SiO2Col-1:end),1))]];
%rearrange formatting...
VolcAverages=[VolcAverages(:,3:4) VolcAverages(:,1:2) VolcAverages(:,locstart:locend) VolcAverages(:,SiO2Col:end)];
%Compile Volcano Metadata
MyMeta=MetaData(1,:);
for i=2:size(VolcAverages,1)
    Newline=MetaData(find(strcmpi(MetaData(:,1),VolcAverages{i,3})),:);
    if size(Newline,1)==0
        Newline=cell(1,25);
    end
    if isempty(Newline{1,1})
         Newline{1,1}='No MetaData Available';
    end
    MyMeta=[MyMeta; Newline];
end
VolcAverages=[VolcAverages MyMeta];
if exist(String2, 'file')==2
    delete(String2)
end
xlswrite(String2,VolcAverages)
end